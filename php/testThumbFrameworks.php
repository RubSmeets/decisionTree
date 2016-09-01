<?php

  /* Read frameworks DB */
  $db_string = file_get_contents("trimmed_frameworks.json");
  $db = json_decode($db_string);

  $data = array(
    "frameworks" => $db
  );

  echo json_encode($data);
  
  return;
  
?>
