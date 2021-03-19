import { identity } from '../util/identity';
import { operate } from '../util/lift';
import { OperatorSubscriber } from './OperatorSubscriber';
export function skipLast(skipCount) {
    return skipCount <= 0
        ? identity
        : operate((source, subscriber) => {
            let ring = new Array(skipCount);
            let count = 0;
            source.subscribe(new OperatorSubscriber(subscriber, (value) => {
                const currentCount = count++;
                if (currentCount < skipCount) {
                    ring[currentCount] = value;
                }
                else {
                    const index = currentCount % skipCount;
                    const oldValue = ring[index];
                    ring[index] = value;
                    subscriber.next(oldValue);
                }
            }, undefined, undefined, () => (ring = null)));
        });
}
//# sourceMappingURL=skipLast.js.map