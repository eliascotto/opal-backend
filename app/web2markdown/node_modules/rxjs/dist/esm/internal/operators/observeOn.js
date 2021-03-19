import { operate } from '../util/lift';
import { OperatorSubscriber } from './OperatorSubscriber';
export function observeOn(scheduler, delay = 0) {
    return operate((source, subscriber) => {
        source.subscribe(new OperatorSubscriber(subscriber, (value) => subscriber.add(scheduler.schedule(() => subscriber.next(value), delay)), (err) => subscriber.add(scheduler.schedule(() => subscriber.error(err), delay)), () => subscriber.add(scheduler.schedule(() => subscriber.complete(), delay))));
    });
}
//# sourceMappingURL=observeOn.js.map