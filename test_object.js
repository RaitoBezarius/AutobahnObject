var auto = require('autobahn');

var connection = new auto.Connection({
	url: 'ws://127.0.0.1:8080/ws',
	realm: 'realm1'
});

connection.onopen = function (session) {
	function onObjectUpdated(args, kwargs, details) {
		console.log('Object updated', {new: args[0]});
	}

	var oID = null;
	session.call('com.objects.create', ['house', {name: 'Ma super maison', price: 15000}], {})
	.then(function (objectId) {
		oID = objectId;
		console.log('Got object ID:', oID);
		return session.call('com.objects.' + objectId + '.get');
	})
	.then(function (object) {
		console.log('Fetched object:', object);
		return session.subscribe('com.objects.' + object.id + '.update', onObjectUpdated);
	})
	.then(function (subscription) {
		console.log('Ready to receive updates for the object.');
		console.log('Publishing on ' + oID);
		return session.publish('com.objects.' + oID + '.update', [{price: 30000}], {}, {acknowledge: true, exclude_me: false});
	})
	.then(function () {
		console.log('Published first update.', arguments);
		session.publish('com.objects.' + oID + '.update', [{name: 'Ma super villa'}], {}, {exclude_me: false});
		console.log('Published second update.');
	})
	.catch(function (error) {
		console.log('Error happened:', error);
	});
}

connection.open();
