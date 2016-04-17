var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/addData', function(req, res) {
    var db = req.db;
    //var students = db.get('people');
});

router.get('/getData', function(req, res) {
    
});

module.exports = router;
