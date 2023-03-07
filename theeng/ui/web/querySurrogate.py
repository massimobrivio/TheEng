from os.path import isfile
from pickle import load
from typing import List

import streamlit as st


class SurrogateView:
    def __init__(self, path: str) -> None:
        st.set_page_config(layout="wide")
        st.title("Surrogate Inspector")
        self.surrogatePath = None
        self.pNames = None
        self.resultNames = None
        self.names = None
        self.designEvaluation = []
        self.path = path

        with st.expander("Settings", expanded=True):
            left, center, right = st.columns((1, 1, 1))
            with left:
                evaluator = self._setSurrogatePath(self.path)
            with center:
                self._setParameters()
            with right:
                self._setTargets()

            self.names = self.pNames + self.resultNames  # type: ignore

        with st.container():
            left_1, right_1 = st.columns((1, 1))
            with left_1:
                numericInputs = self._getInputs(self.pNames)  # type: ignore
                predictButton = st.button("Predict")
            with right_1:
                if predictButton:
                    if evaluator:
                        resultList = evaluator(numericInputs)  # type: ignore
                        self._getOutputs(self.resultNames, resultList)  # type: ignore

    def _setSurrogatePath(self, path: str):
        self.surrogatePath = st.text_input("Path to surrogate", path)
        if isfile(self.surrogatePath):
            with open(self.surrogatePath, "rb") as surrogateFile:
                surrogate = load(surrogateFile)  # type: ignore

            def evaluator(parameterValues):
                return surrogate.predict([parameterValues])

            return evaluator
        else:
            st.error("Surrogate file does not exist. Check path and filename.")
            return None

    def _setParameters(self):
        parametersString = st.text_input(
            "Parameters name"
        )  # todo: use parameters from main script if available as default
        self.pNames = parametersString.replace(" ", "").split(",")

    def _setTargets(self):
        resultNamesString = st.text_input(
            "Results name"
        )  # todo: use results from main script if available as default
        self.resultNames = resultNamesString.replace(" ", "").split(",")

    def _getInputs(self, inputsList: List[str]) -> List[float]:
        inputsList = list(filter(None, inputsList))
        numericInputs = []
        for count, input in enumerate(inputsList):
            numericInputs.append(st.number_input(input, key=count))
        return numericInputs

    def _getOutputs(self, outputsList: List[str], resultList: List[List[float]]):
        outputsList = list(filter(None, outputsList))
        textOutputs = []
        for output in zip(outputsList, resultList[0]):
            textOutputs.append(st.metric(output[0], output[1]))


if __name__ == "__main__":
    view = SurrogateView(
        path="C:\\Repositories\\TheEng\\examples\\beam_freecad_multiobj\\surrogate.pkl"
    )
