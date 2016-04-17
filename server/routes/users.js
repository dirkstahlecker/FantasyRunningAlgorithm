var express = require('express');
var router = express.Router();

router.get('/', function(req, res) {
  var db = req.db;
  var students = db.get('people');
  students.find({}, function(e, docs){
  	res.render('users/index', { title: 'Users', 'individuals': docs });
  });
});

router.get('/new', function(req, res) {
	res.render('users/new', { title: 'Add New User' });
});

router.post('/create', function(req, res, next) {
	var db = req.db;
  	var students = db.get('people');
	students.insert({"name": req.body.user, "age": req.body.user_age}, function(err, docs){
		if(err){
			res.send("There was a problem");
		}else{
			res.redirect("/users");
		}
	});
});

module.exports = router;
