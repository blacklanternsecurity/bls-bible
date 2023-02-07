<!---------------------------------------------------------------------------------
Copyright: (c) BLS OPS LLC.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------->
function Get-ApplicationHost {
	$OrigError = $ErrorActionPreference
	$ErrorActionPreference = "SilentlyContinue"
​
	# Check if appcmd.exe exists
	if (Test-Path  ("$Env:SystemRoot\System32\inetsrv\appcmd.exe")) {
		# Create data table to house results
		$DataTable = New-Object System.Data.DataTable
​
		# Create and name columns in the data table
		$Null = $DataTable.Columns.Add("user")
		$Null = $DataTable.Columns.Add("pass")
		$Null = $DataTable.Columns.Add("type")
		$Null = $DataTable.Columns.Add("vdir")
		$Null = $DataTable.Columns.Add("apppool")
​
		# Get list of application pools
		Invoke-Expression "$Env:SystemRoot\System32\inetsrv\appcmd.exe list apppools /text:name" | ForEach-Object {
​
			# Get application pool name
			$PoolName = $_
​
			# Get username
			$PoolUserCmd = "$Env:SystemRoot\System32\inetsrv\appcmd.exe list apppool " + "`"$PoolName`" /text:processmodel.username"
			$PoolUser = Invoke-Expression $PoolUserCmd
​
			# Get password
			$PoolPasswordCmd = "$Env:SystemRoot\System32\inetsrv\appcmd.exe list apppool " + "`"$PoolName`" /text:processmodel.password"
			$PoolPassword = Invoke-Expression $PoolPasswordCmd
​
			# Check if credentials exists
			if (($PoolPassword -ne "") -and ($PoolPassword -isnot [system.array])) {
				# Add credentials to database
				$Null = $DataTable.Rows.Add($PoolUser, $PoolPassword,'Application Pool','NA',$PoolName)
			}
		}
​
		# Get list of virtual directories
		Invoke-Expression "$Env:SystemRoot\System32\inetsrv\appcmd.exe list vdir /text:vdir.name" | ForEach-Object {
​
			# Get Virtual Directory Name
			$VdirName = $_
​
			# Get username
			$VdirUserCmd = "$Env:SystemRoot\System32\inetsrv\appcmd.exe list vdir " + "`"$VdirName`" /text:userName"
			$VdirUser = Invoke-Expression $VdirUserCmd
​
			# Get password
			$VdirPasswordCmd = "$Env:SystemRoot\System32\inetsrv\appcmd.exe list vdir " + "`"$VdirName`" /text:password"
			$VdirPassword = Invoke-Expression $VdirPasswordCmd
​
			# Check if credentials exists
			if (($VdirPassword -ne "") -and ($VdirPassword -isnot [system.array])) {
				# Add credentials to database
				$Null = $DataTable.Rows.Add($VdirUser, $VdirPassword,'Virtual Directory',$VdirName,'NA')
			}
		}
​
		# Check if any passwords were found
		if( $DataTable.rows.Count -gt 0 ) {
			# Display results in list view that can feed into the pipeline
			$DataTable |  Sort-Object type,user,pass,vdir,apppool | Select-Object user,pass,type,vdir,apppool -Unique
		}
		else {
			# Status user
			Write-Verbose 'No application pool or virtual directory passwords were found.'
			$False
		}
	}
	else {
		Write-Verbose 'Appcmd.exe does not exist in the default location.'
		$False
	}
	$ErrorActionPreference = $OrigError
}