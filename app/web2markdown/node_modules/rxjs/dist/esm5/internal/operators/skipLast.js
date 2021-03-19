import { identity } from '../util/identity';
import { operate } from '../util/lift';
import { OperatorSubscriber } from './OperatorSubscriber';
export function skipLast(skipCount) {
    return skipCount <= 0
        ? identity
        : operate(function (source, subscriber) {
            var ring = new Array(skipCount);
            var count = 0;
            source.subscribe(new OperatorSubscriber(subscriber, function (value) {
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
//# sourceMappingURL=skipLast.js.map