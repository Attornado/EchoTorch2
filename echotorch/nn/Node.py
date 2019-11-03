# -*- coding: utf-8 -*-
#
# File : echotorch/nn/Node.py
# Description : Basis node for EchoTorch.
# Date : 29th of October, 2019
#
# This file is part of EchoTorch.  EchoTorch is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Nils Schaetti <nils.schaetti@unine.ch>

"""
Created on 29 October 2019
@author: Nils Schaetti
"""

import torch
import torch.sparse
import torch.nn as nn
import numpy as np


# Basis node for EchoTorch
class Node(nn.Module):
    """
    Basis node for EchoTorch
    """

    # Debug mode
    NO_DEBUG = 0
    DEBUG_TEST = 1
    DEBUG_OUTPUT = 2
    DEBUG_TEST_CASE = 3

    # Constructor
    def __init__(self, input_dim, output_dim, debug=NO_DEBUG, test_case=None, dtype=torch.float32):
        """
        Constructor
        :param input_dim: Node's input dimension.
        :param output_dim: Node's output dimension.
        :param debug: Set debug mode
        :param test_case: Test case to call.
        :param dtype: Node's type.
        """
        # Superclass
        super(Node, self).__init__()

        # Params
        self._input_dim = input_dim
        self._output_dim = output_dim
        self._debug = debug
        self._dtype = dtype

        # Debug points and test
        self._debug_points = dict()
        self._test_case = test_case

        # Handlers
        self._neural_filter_handler = None
    # end __init__

    #######################
    # Properties
    #######################

    # Input dimension
    @property
    def input_dim(self):
        """
        Get input dimension
        """
        return self._input_dim
    # end input_dim

    # Set input dimension
    @input_dim.setter
    def input_dim(self, new_dim):
        """
        Set input dimension
        :param new_dim: New input dimension
        """
        self._input_dim = new_dim
    # end input_dim

    # Output dimension
    @property
    def output_dim(self):
        """
        Get output dimension
        """
        return self._output_dim

    # end input_dim

    # Set output dimension
    @output_dim.setter
    def output_dim(self, new_dim):
        """
        Set output dimension
        :param new_dim: New output dimension
        """
        self._output_dim = new_dim
    # end output_dim

    # Type
    @property
    def dtype(self):
        """
        Type
        :return: Type
        """
        return self._dtype
    # end dtype

    # Is the layer trainable?
    @property
    def is_trainable(self):
        """
        Is the node trainable ?
        :return: True/False
        """
        return False
    # end is_trainable

    # Is the layer invertible ?
    @property
    def is_invertibe(self):
        """
        Is the layer invertible ?
        :return: True/False
        """
        return False
    # end is_invertible

    # Supported dtypes
    @property
    def supported_dtype(self):
        """
        Supported dtypes
        """
        return [torch.float16, torch.float32, torch.float64]
    # end supported_dtype

    #######################
    # Forward/Backward/Init
    #######################

    # Reset learning
    def reset(self):
        """
        Reset learning
        :return:
        """
        # Training mode again
        self.train(True)
    # end reset

    # Forward
    def forward(self, *input):
        """
        Forward
        :param input:
        :return:
        """
        pass
    # end forward

    # Finish training
    def finalize(self):
        """
        Finish training
        """
        pass
    # end finalize

    # Initialization of the node
    def initialize(self):
        """
        Initialization of the node
        """
        pass
    # end initialize

    #######################
    # Public
    #######################

    # Set debug mode
    def debug(self, mode):
        """
        Set debug mode
        :param mode: True/False
        """
        self._debug = mode
    # end debug

    # Set a debug point
    def debug_point(self, name, value, precision):
        """
        Set a debug point for comparison
        :param name: Name of the debug point (corresponding to one given by the module)
        :param value: Value of the debug point to compare (ex, matrix, scalar, etc)
        :param precision: Limit precision.
        """
        self._debug_points[name] = (value, precision)
    # end debug_point

    # Connect handler
    def connect(self, handler_name, handler_func):
        """
        Connect handler
        :paramm handler_name: Handler name
        :param handler_func: Handler function
        """
        if handler_name == "neural-filter":
            self._neural_filter_handler = handler_func
        # end if
    # end connect

    #######################
    # Numerical operations
    #######################

    # Matrix inverse
    def _inverse(self, name, M):
        """
        Matrix inverse
        :param name: Name associated with M
        :param M: Matrix to inverse
        :return: Inverse matrix
        """
        if self._debug == Node.DEBUG_TEST or self._debug == Node.DEBUG_OUTPUT:
            # SVD of matrix
            _, S, _ = torch.svd(M)

            # Condition number
            condition_number = torch.log10(S[0] / S[-1])

            # Show condition number
            if self._debug == Node.DEBUG_OUTPUT:
                print(
                    "DEBUG - INFO : Condition number while inversing {} : {}".format(
                        name,
                        condition_number
                    )
                )

            # Bad condition number
            if condition_number > 14:
                print(
                    "DEBUG - WARNING : High condition number while inversing {} : {}".format(
                        name,
                        condition_number
                    )
                )
            # end if
        # end if
        return torch.inverse(M)
    # end _inverse

    # Matrix pseudo-inverse
    def _pinverse(self, name, M):
        """
        Matrix pseudo-inverse
        :param name: Name associated with M
        :param M: Matrix to inverse
        :return: Pseudo-inverse of matrix
        """
        if self._debug == Node.DEBUG_TEST or self._debug == Node.DEBUG_OUTPUT:
            # SVD of matrix
            _, S, _ = torch.svd(M)

            # Condition number
            condition_number = torch.log10(S[0] / S[-1])

            # Show condition number
            if self._debug == Node.DEBUG_OUTPUT:
                print(
                    "DEBUG - INFO : Condition number while pseudo-inversing {} : {}".format(
                        name,
                        condition_number
                    )
                )

            # Bad condition number
            if condition_number > 14:
                print(
                    "DEBUG - WARNING : High condition number while pseudo-inversing {} : {}".format(
                        name,
                        condition_number
                    )
                )
            # end if
        # end if
        return torch.pinverse(M)
    # end _pinverse

    #######################
    # Private
    #######################

    # Call debug point
    def _call_debug_point(self, name, value):
        """
        Call a debug point from inside the module to compare with given values
        :param name: Name of the debug point
        :param value: Value of the debug point
        """
        # String
        error_precision = "DEBUG - ERROR: {} have precision issue! (module:{}, outside:{})"
        info_precision_scalar = "DEBUG - INFO: {} (scalar) has an absolute difference of {}"
        info_precision_matrix = "DEBUG - INFO: {} (matrix) has a norm-2 difference of {}"
        fatal_size = "DEBUG - FATAL: {} have not the same size! (module:{}, outside:{})"
        fatal_type = "DEBUG - FATAL: {} are not of the same type! (module:{}, outside:{})"

        # If debug point set
        if self._debug > Node.NO_DEBUG and name in self._debug_points.keys():
            # Get value
            value_from_module = value
            value_from_outside, precision = self._debug_points[name]

            # Test same type
            if type(value_from_module) == type(value_from_outside):
                # Type scalar
                if isinstance(value_from_module, int) or isinstance(value_from_module, float):
                    # Compute absolute difference
                    abs_diff = np.abs(value_from_module - value_from_outside)

                    # In debug output, print difference
                    if self._debug == Node.DEBUG_OUTPUT or self._debug == Node.DEBUG_TEST_CASE:
                        print(info_precision_scalar.format(name, abs_diff))
                    # end if

                    # In debug test case, call test call for evaluation
                    if self._debug == Node.DEBUG_TEST_CASE:
                        self._test_case.assertAlmostEqual(value_from_module, value_from_outside, precision)
                    # In debut test, test if precision is ok
                    elif abs_diff > precision:
                        print(error_precision.format(name, value_from_module, value_from_outside))
                    # end if
                # Matrix/Tensor
                elif isinstance(value_from_module, torch.Tensor):
                    # Test size
                    if value_from_module.size() == value_from_outside.size():
                        # Compute Frobenius norm difference
                        norm_diff = torch.norm(value_from_module - value_from_outside)

                        # In debug output, print difference
                        if self._debug == Node.DEBUG_OUTPUT or self._debug == Node.DEBUG_TEST_CASE:
                            print(info_precision_matrix.format(name, norm_diff))
                        # end if

                        # In debug test case, call test case for evaluation
                        if self._debug == Node.DEBUG_TEST_CASE:
                            self._test_case.assertTensorAlmostEqual(value_from_module, value_from_outside, precision)
                        if norm_diff > precision:
                            print(error_precision.format(name, torch.norm(value_from_module), torch.norm(value_from_outside)))
                        # end if
                    else:
                        print(fatal_size.format(name, value_from_module.size(), value_from_outside.size()))
                        raise Exception()
                # end if
            else:
                print(fatal_type.format(name, type(value_from_module), type(value_from_outside)))
                raise Exception()
            # end if
        # end if
    # end _call_debug_point

    # Hook which gets executed before the update state equation for every sample.
    def _pre_update_hook(self, inputs, sample_i):
        """
        Hook which gets executed before the update equation for a batch
        :param inputs: Input signal.
        :param sample_i: Batch position.
        """
        return inputs
    # end _pre_update_hook

    # Hook which gets executed before the update state equation for every timesteps.
    def _pre_step_update_hook(self, inputs, t):
        """
        Hook which gets executed before the update equation for every timesteps
        :param inputs: Input signal.
        :param t: Timestep.
        """
        return inputs
    # end _pre_step_update_hook

    # Hook which gets executed after the update state equation for every sample.
    def _post_update_hook(self, states, inputs, sample_i):
        """
        Hook which gets executed after the update equation for a batch
        :param states: Reservoir's states.
        :param inputs: Input signal.
        :param sample_i: Batch position.
        """
        return states
    # end _post_update_hook

    # Hook which gets executed after the update state equation for every timesteps.
    def _post_step_update_hook(self, states, inputs, t):
        """
        Hook which gets executed after the update equation for every timesteps
        :param states: Reservoir's states.
        :param inputs: Input signal.
        :param t: Timestep.
        """
        return states
    # end _post_step_update_hook

# end Node