<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);

$mysqli = new mysqli('172.16.239.11', 'root', 'password', 'vulnerable_db');
if ($mysqli->connect_error) {
    die('Connect Error (' . $mysqli->connect_errno . ') ' . $mysqli->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    $query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
    $result = $mysqli->query($query);
    
    if ($result === false) {
        die("Query failed: " . $mysqli->error);
    }
    
    if ($result->num_rows > 0) {
        $_SESSION['loggedin'] = true;
        $_SESSION['username'] = $username;
        echo "Welcome, admin!";
    } else {
        echo "Invalid login";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="post" action="">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>