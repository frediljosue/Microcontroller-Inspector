// Local PeerJS signalling server used by the phone-camera test (the real app uses the free public server).
const { PeerServer } = require('peer');
PeerServer({ port: 9000, path: '/myapp', host: '127.0.0.1' });
console.log('PeerJS test server on http://127.0.0.1:9000/myapp');
