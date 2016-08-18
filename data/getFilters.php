<?php
	$filters = json_decode(file_get_contents('filters.txt', true));

	if(isset($_GET['callback'])) {
		//Specify the content type to be returned
		//$this->output->set_content_type('application/json');
		header('Content-Type: application/json');
		echo $_GET['callback'] . '(' .json_encode($filters). ')';
	} else {
		echo json_encode($filters);
	}
?>
