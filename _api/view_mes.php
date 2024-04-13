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

// Fetch the message from the database
$sql = "SELECT message FROM messages WHERE id = 1"; // Assuming the message is stored with id = 1
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Output data of each row
    while($row = $result->fetch_assoc()) {
        echo "Message: " . $row["message"];
    }
} else {
    echo "No message found.";
}

// Close connection
$conn->close();

?>
