<?php

$servername = "localhost";
$username = "1234";
$password = "1234";
$database = "1234";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Handle POST request to update message
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize input
    $message = $conn->real_escape_string($_POST["message"]);

    // Update the message in the database
    $sql = "UPDATE messages SET message = '$message' WHERE id = 1"; // Assuming there's only one message in the table
    if ($conn->query($sql) === TRUE) {
        echo json_encode(array("status" => "success", "message" => "Message updated successfully"));
    } else {
        echo json_encode(array("status" => "error", "message" => "Error updating message: " . $conn->error));
    }
} else {
    echo json_encode(array("status" => "error", "message" => "Only POST requests are allowed"));
}

// Close connection
$conn->close();

?>
