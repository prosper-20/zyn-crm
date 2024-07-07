</?php
$ servername = "localhost";
$ username = "root";
$ password = "root";
$ conn = mysql($servername, $username, $password)

if ($conn->connect_error) {
    die("Connection failed".$conn->connect.error);
}
echo "Connected successfully" 
?>


<!-- SECOND PART": WITH A DATABASE -->

$sql = "CREATE DATABASE Test"
if ($conn->query($sql) === TRUE) {
    echo "Database created successfully";
    } else {
        echo "Error creating database: " . $conn->error;
        }
        $conn->close();

