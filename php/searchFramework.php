<?php
    
    if(isset($_GET["keyword"])) {
        $searchWord = $_GET["keyword"];
    }
    
    echo json_encode($searchWord);
?>