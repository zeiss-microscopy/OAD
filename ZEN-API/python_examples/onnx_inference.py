# -*- coding: utf-8 -*-

#################################################################
# File        : onnx_inference.py
# Author      : sebi06, Team Enchilada
#
# Disclaimer: This code is purely experimental. Feel free to
# use it at your own risk.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from typing import Tuple, Optional, List, cast
from types import TracebackType

import numpy as np
import torch
import onnxruntime as rt


class ManagedOnnxSession:
    """Context manager for ONNX models."""

    def __init__(self, model_path: str, providers: Optional[List[str]] = None) -> None:
        """Creates an instance of the context manager.

        Arguments:
            model_path: The path to the model on disk.
            providers: The names of the provider classes to be used to retrieve an execution device.
        """
        self._model_path = model_path
        self.providers = providers

    def __enter__(self) -> rt.InferenceSession:
        """Creates an ONNX inference session."""
        self._session = rt.InferenceSession(self._model_path, providers=self.providers)
        return self._session

    def __exit__(
        self, exc_type: BaseException, exc_val: BaseException, exc_tb: TracebackType
    ) -> None:
        """Deletes the ONNX inference session."""
        del self._session


class OnnxInferencer:
    """Inferencer class to load and evaluate models in ONNX format."""

    def __init__(self, model_path: str) -> None:
        """Creates an instance of a ONNX inferencer.

        Arguments:
            model_path: The path to the model on disk.
        """
        super().__init__()
        self._model_path = model_path

    def predict(self, x: List[np.ndarray], use_gpu: bool = False) -> List[np.ndarray]:
        """Evaluates the underlying model with the given input _data.

        Arguments:
            x: The input _data to evaluate the model with.
            use_gpu: Allow execution on GPU (True) or enforce CPU execution (False).

        Returns:
            The prediction for the given input _data.
        """

        def predict_one(
            sess: rt.InferenceSession, batch_elem: np.ndarray
        ) -> np.ndarray:
            """Predicts with a batch size of 1 to not risk memory issues.

            Arguments:
                sess: The inference session containing the loaded model.
                batch_elem: One element of a batch to be used for prediction.

            Returns:
                The prediction for the provided batch element.
            """
            batch_elem = batch_elem[np.newaxis]
            input_name = sess.get_inputs()[0].name
            output_name = sess.get_outputs()[0].name

            # ONNX can only handle float32
            batch_elem = batch_elem.astype(np.float32)
            input_dict = {input_name: batch_elem}
            result = sess.run([output_name], input_dict)[0]

            if len(result) != 1:
                raise AssertionError(
                    "The batch size has changed during ANN model execution"
                )
            return result[0]

        def _predict_batch(
            _x: List[np.ndarray], use_gpu: bool = True
        ) -> List[np.ndarray]:
            """Run prediction on a batch of images.

            Arguments:
                _x: The batch of images to be predicted.
                use_gpu: Allow execution on GPU (True) or enforce CPU execution (False).

            Returns:
                 The predictions for the given batch of images.
            """

            # try to make it run fast with GPU
            # https://medium.com/neuml/debug-onnx-gpu-performance-c9290fe07459

            with ManagedOnnxSession(
                self._model_path,
                providers=(
                    [
                        (
                            "CUDAExecutionProvider",
                            {"cudnn_conv_algo_search": "DEFAULT"},
                        ),
                        "CPUExecutionProvider",
                    ]
                    if use_gpu
                    else ["CPUExecutionProvider"]
                ),
            ) as sess:

                # We predict with a batch size of 1 to not risk memory issues
                prediction_list = [predict_one(sess, batch_elem) for batch_elem in _x]

                return prediction_list

        return _predict_batch(x, use_gpu=use_gpu)

    def get_input_shape(self) -> Tuple[int, int, int, int]:
        """Determines the input shape expected by the loaded model.

        Using CPUExecutionProvider straight from the first run to not try-except for CUDAExecutionProvider - fast op.

        Returns:
            The expected input shape.
        """
        with ManagedOnnxSession(
            self._model_path, providers=["CPUExecutionProvider"]
        ) as sess:
            input_shape = tuple(
                elem if isinstance(elem, int) else None
                for elem in sess.get_inputs()[0].shape
            )
            if len(input_shape) != 4:
                raise ValueError(
                    f"The input shape of the model must have four dimensions. Found dimensions: {input_shape}"
                )
            return cast(Tuple[int, int, int, int], input_shape)

    def get_output_shape(
        self,
    ) -> Tuple[Optional[int], Optional[int], Optional[int], Optional[int]]:
        """Determines the output shape of the loaded model.

        Using CPUExecutionProvider straight from the first run to not try-except for CUDAExecutionProvider - fast op.

        Returns:
            The output shape of the model.
        """
        with ManagedOnnxSession(
            self._model_path, providers=["CPUExecutionProvider"]
        ) as sess:
            output_shape = tuple(
                elem if isinstance(elem, int) else None
                for elem in sess.get_outputs()[0].shape
            )
            if len(output_shape) != 4:
                raise ValueError(
                    f"The output shape of the model must have four dimensions. Found dimensions: {output_shape}"
                )
            return cast(
                Tuple[Optional[int], Optional[int], Optional[int], Optional[int]],
                output_shape,
            )
