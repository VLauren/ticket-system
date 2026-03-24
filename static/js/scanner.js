
let scanned = false;

function onScanSuccess(decodedText)
{
	if(scanned) return;

	scanned = true;
	const ticketId = decodedText;
	window.location.href = "/ticket/" + ticketId + "?day=" + scanDay;
}

const scanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250});

scanner.render(onScanSuccess);
