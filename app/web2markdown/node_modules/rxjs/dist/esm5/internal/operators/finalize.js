import { operate } from '../util/lift';
export function finalize(callback) {
    return operate(function (source, subscriber) {
        source.subscribe(subscriber);
        subscriber.add(callback);
    });
}
//# sourceMappingURL=finalize.js.map