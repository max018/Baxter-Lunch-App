<?php
	
	$url = 'http://127.0.0.1/cmty/_baxter/lunch_repo/-workspace/php%20bypass/relay.php';

	$data_string = file_get_contents('php://input');

	$ch = curl_init($url);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
	curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array(
	    'Content-Type: application/json',
	    'Content-Length: ' . strlen($data_string))
	);

	$result = curl_exec($ch);

	echo $result;