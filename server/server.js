const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());

app.use(express.json());

app.delete('/destination/:id', (req, res) => {
  const { id } = req.params; 
  console.log(`Deleting destination with ID: ${id}`);

  
  res.send({ message: `Destination with ID ${id} deleted` });
});


app.listen(5555, () => {
  console.log('Server running on port 5555');
});
