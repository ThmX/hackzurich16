const express = require('express');
let router = express.Router();

const _ = require('lodash');

const data = _.flatten([
    require('../data/356156068026087_2016-09-01.json'),
    require('../data/356156068026087_2016-09-02.json'),
    require('../data/356156068026087_2016-09-03.json'),
    require('../data/356156068026087_2016-09-04.json'),
    require('../data/356156068026087_2016-09-05.json'),
    require('../data/356156068026087_2016-09-06.json'),
    require('../data/356156068026087_2016-09-07.json'),
    require('../data/356156068026087_2016-09-08.json'),
    require('../data/356156068026087_2016-09-09.json'),
    require('../data/356156068026087_2016-09-10.json'),
    require('../data/356156068026087_2016-09-11.json'),
    require('../data/356156068026087_2016-09-12.json'),
    require('../data/356156068026087_2016-09-13.json'),
    require('../data/356156068026087_2016-09-14.json'),
    require('../data/356156068026087_2016-09-15.json'),
    require('../data/356156068026087_2016-09-16.json'),
    require('../data/356156068030410_2016-09-05.json'),
    require('../data/356156068030410_2016-09-06.json'),
    require('../data/356156068030410_2016-09-07.json'),
    require('../data/356156068030410_2016-09-08.json'),
    require('../data/356156068030410_2016-09-09.json'),
    require('../data/356156068030410_2016-09-10.json'),
    require('../data/356156068030410_2016-09-11.json'),
    require('../data/356156068030410_2016-09-12.json'),
    require('../data/356156068030410_2016-09-13.json'),
    require('../data/356156068030410_2016-09-14.json'),
    require('../data/356156068030410_2016-09-15.json'),
    require('../data/356156068030410_2016-09-16.json')
]);

router.get('/', (req, res, next) => {
    res.send(_.uniq(_.map(data, 'asset')));
});

router.get('/:asset/:fromDate', (req, res, next) => {
    const asset = req.params.asset;
    const fromDate = new Date(req.params.fromDate).getDate();
    res.send(_.filter(_.filter(data, {'asset': asset}), evt => {
        const check = new Date(evt.recorded_at * 1000).getDate();
        return fromDate <= check;
    }));
});

router.get('/:asset/:fromDate/:toDate', (req, res, next) => {
    const asset = req.params.asset;
    const fromDate = new Date(req.params.fromDate).getDate();
    const toDate = new Date(req.params.toDate).getDate();
    res.send(_.filter(_.filter(data, {'asset': asset}), evt => {
        const check = new Date(evt.recorded_at * 1000).getDate();
        return fromDate <= check && check <= toDate;
    }));
});

module.exports = router;
