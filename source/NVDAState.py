# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import sys
import time

import globalVars


def isRunningAsSource() -> bool:
	"""
	True if NVDA is running as a source copy.
	When running as an installed copy, py2exe sets sys.frozen to 'windows_exe'.
	"""
	return getattr(sys, 'frozen', None) is None


def _allowDeprecatedAPI() -> bool:
	"""
	Used for marking code as deprecated.
	This should never be False in released code.

	Making this False may be useful for testing if code is compliant without using deprecated APIs.
	Note that deprecated code may be imported at runtime,
	and as such, this value cannot be changed at runtime to test compliance.
	"""
	return True


def getStartTime() -> float:
	return globalVars.startTime


def _initializeStartTime() -> None:
	assert globalVars.startTime == 0
	globalVars.startTime = time.time()


def _getExitCode() -> int:
	return globalVars.exitCode


def _setExitCode(exitCode: int) -> None:
	globalVars.exitCode = exitCode


class _TrackNVDAInitialization:
	"""
	During NVDA initialization,
	core._initializeObjectCaches needs to cache the desktop object,
	regardless of lock state.
	Security checks may cause the desktop object to not be set if NVDA starts on the lock screen.
	As such, during initialization, NVDA should behave as if Windows is unlocked,
	i.e. winAPI.sessionTracking._isLockScreenModeActive should return False.
	"""

	_isNVDAInitialized = False
	"""When False, _isLockScreenModeActive is forced to return False.
	"""

	@staticmethod
	def markInitializationComplete():
		assert not _TrackNVDAInitialization._isNVDAInitialized
		_TrackNVDAInitialization._isNVDAInitialized = True

	@staticmethod
	def isInitializationComplete() -> bool:
		return _TrackNVDAInitialization._isNVDAInitialized
