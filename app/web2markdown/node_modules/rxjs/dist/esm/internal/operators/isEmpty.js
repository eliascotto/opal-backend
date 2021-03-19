import { operate } from '../util/lift';
import { OperatorSubscriber } from './OperatorSubscriber';
export function isEmpty() {
    return operate((source, subscriber) => {
        source.subscribe(new OperatorSubscriber(subscriber, () => {
            subscriber.next(false);
            subscriber.complete();
        }, undefined, () => {
            subscriber.next(true);
            subscriber.complete();
        }));
    });
}
//# sourceMappingURL=isEmpty.js.map