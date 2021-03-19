import { Notification } from '../Notification';
import { operate } from '../util/lift';
import { OperatorSubscriber } from './OperatorSubscriber';
export function materialize() {
    return operate(function (source, subscriber) {
        source.subscribe(new OperatorSubscriber(subscriber, function (value) {
            subscriber.next(Notification.createNext(value));
        }, function (err) {
            subscriber.next(Notification.createError(err));
            subscriber.complete();
        }, function () {
            subscriber.next(Notification.createComplete());
            subscriber.complete();
        }));
    });
}
//# sourceMappingURL=materialize.js.map