# -*- coding: utf-8 -*-
#
# File : echotorch/datasets/EchoDataset.py
# Description : Base class for EchoTorch datasets
# Date : 25th of January, 2021
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


# Imports
from typing import Union, List
import torch
from torch.utils.data.dataset import Dataset


# EchoDataset
class EchoDataset(Dataset):
    r"""An abstract class for EchoTorch dataset objects
    """

    # region CONSTRUCTORS

    # Constructors
    def __init__(
            self,
            n: int,
            stream: bool
    ) -> None:
        r"""Constructors

        Args:
            n: The size of the data set (number of samples)
            stream: Do we generate samples on the fly?
        """
        # Properties
        self._n = n
        self._stream = stream
    # end __init__

    # endregion CONSTRUCTORS

    # region OVERRIDE

    # Length
    def __len__(self):
        r"""Get the length of the dataset

        Returns: The length of the dataset (Scalar)

        """
        return self._n
    # end __len__

    # Representation
    def __repr__(self):
        r"""Returns a displayable representation of the object

        Returns:
            A displayable representation of the object

        """
        return "{}({})".format(
            self.__class__.__name__,
            self.extra_repr()
        )
    # end __repr__

    # endregion OVERRIDE

    # region TO_IMPLEMENT

    # Get the whole dataset
    @property
    def data(self) -> Union[torch.Tensor, List]:
        """
        Get the whole dataset (according to init parameters)
        @return: The Torch Tensor
        """
        raise Exception("data not implemented")
    # end data

    # Extra representation
    def extra_repr(self) -> str:
        """
        Extra representation
        """
        raise Exception("extra_repr not implemented")
    # end extra_repr

    # Function to generate data
    def datafunc(self, *args, **kwargs):
        """
        Function to generate data
        :param args: Positional arguments
        :param kwargs: Arguments
        """
        raise Exception("datafunc not implemented")
    # end datafunc

    # endregion TO_IMPLEMENT

# end EchoDataset
