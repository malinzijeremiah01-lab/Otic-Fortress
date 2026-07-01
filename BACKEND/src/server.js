const express = require("express");

const app = express();

app.use(express.json());

app.get("/health", (req, res) => {
    res.json({
        status: "ok",
        system: "Fortress"
    });
});

const PORT = 3000;

app.listen(PORT, () => {
    console.log(`Fortress backend running on port ${PORT}`);
});