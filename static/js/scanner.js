function onScanSuccess(decodedText)
{
	const ticketId = decodedText;
	window.location.href = "/ticket/" + ticketId
}

const scanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250});

scanner.render(onScanSuccess);
