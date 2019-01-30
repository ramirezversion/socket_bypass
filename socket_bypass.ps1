param( [string] $remoteHost = "192.168.56.101", [int] $port = 443)   

try
{
	Write-Host "Connecting to $remoteHost on port $port ... " -NoNewLine
	try
	{
		$socket = New-Object System.Net.Sockets.TcpClient( $remoteHost, $port )
		Write-Host -ForegroundColor Green "OK"
	}
	catch
	{
		Write-Host -ForegroundColor Red "failed"
		exit -1
	}

	$stream = $socket.GetStream( )
	#$writer = New-Object System.IO.StreamWriter( $stream )
	$buffer = New-Object System.Byte[] 1024
	$encoding = New-Object System.Text.AsciiEncoding
    $data = ""

	start-sleep -m 500
	while( $stream.DataAvailable )
	{
		$read = $stream.Read( $buffer, 0, 1024 )
        $data = $data + $read
		#Write-Host -n ($encoding.GetString( $buffer, 0, $read ))
            
	}

}
finally
{
	#if( $writer ) {	$writer.Close( )	}
	if( $stream ) {	$stream.Close( )	}
    Write-Host -n  ($encoding.GetString( $buffer, 0, $data ))
} 