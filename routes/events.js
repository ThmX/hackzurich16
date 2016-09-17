var express = require('express');
var _ = require('lodash');

var data = require('../data/356156068026087_2016-09-01.json');

let router = express.Router();

router.get('/', (req, res, next) => {
    res.send(_.uniq(_.map(data, 'asset')));
});

router.get('/:asset', (req, res, next) => {
    const asset = req.params.asset;
    res.send(_.filter(data, {'asset': asset}));
});

module.exports = router;
