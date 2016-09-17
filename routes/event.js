var express = require('express');
var router = express.Router();

router.get('/:eventID', function (req, res, next) {
    const id = req.params.eventID;
    res.send(id);
});

module.exports = router;
