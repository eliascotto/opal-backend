"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.skipLast = void 0;
var identity_1 = require("../util/identity");
var lift_1 = require("../util/lift");
var OperatorSubscriber_1 = require("./OperatorSubscriber");
function skipLast(skipCount) {
    return skipCount <= 0
        ? identity_1.identity
        : lift_1.operate(function (source, subscriber) {
            var ring = new Array(skipCount);
            var count = 0;
            source.subscribe(new OperatorSubscriber_1.OperatorSubscriber(subscriber, function (value) {
                var currentCount = count++;
                if (currentCount < skipCount) {
                    ring[currentCount] = value;
                }
                else {
                    var index = currentCount % skipCount;
                    var oldValue = ring[index];
                    ring[index] = value;
                    subscriber.next(oldValue);
                }
            }, undefined, undefined, function () {
                return (ring = null);
            }));
        });
}
exports.skipLast = skipLast;
//# sourceMappingURL=skipLast.js.map