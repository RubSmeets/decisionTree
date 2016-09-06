<?php
    
    if(isset($_GET["keyword"])) {
        $searchWord = $_GET["keyword"];
    }

    /* Read frameworks DB */
    $db_string = file_get_contents("framework_compare.json");
    $frameworkArray = json_decode($db_string, true); // create array from json

    $response = "";
    /* Loop over array items */
    foreach($frameworkArray as $framework) {
        /* loop over framework fields */
        $tempName = $framework["framework"];
        if(strcmp(strtolower($searchWord),strtolower($tempName)) == 0) {
            $response = $framework;
            break;
        }
    }

    /* Return response and warning when empty */
    if (empty($response)) {
        $resp = 'response is either 0, empty, or not set at all';
        echo json_encode($resp);
    } else {
        echo json_encode($response);
    }
?>