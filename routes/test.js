var express = require('express');
var router = express.Router();

var _ = require('lodash');

var rawTest = require('../data/356156068026087_2016-09-01_raw.json');

/* GET home page. */
router.get('/', (req, res, next) => {

    res.send('');

});

module.exports = router;
