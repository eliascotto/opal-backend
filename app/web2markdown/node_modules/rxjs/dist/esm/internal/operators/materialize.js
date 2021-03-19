import { Notification } from '../Notification';
import { operate } from '../util/lift';
import { OperatorSubscriber } from './OperatorSubscriber';
export function materialize() {
    return operate((source, subscriber) => {
        source.subscribe(new OperatorSubscriber(subscriber, (value) => {
            subscriber.next(Notification.createNext(value));
        }, (err) => {
            subscriber.next(Notification.createError(err));
            subscriber.complete();
        }, () => {
            subscriber.next(Notification.createComplete());
            subscriber.complete();
        }));
    });
}
//# sourceMappingURL=materialize.js.map