import { operate } from '../util/lift';
import { noop } from '../util/noop';
import { OperatorSubscriber } from './OperatorSubscriber';
import { innerFrom } from '../observable/from';
export function bufferWhen(closingSelector) {
    return operate((source, subscriber) => {
        let buffer = null;
        let closingSubscriber = null;
        const openBuffer = () => {
            closingSubscriber === null || closingSubscriber === void 0 ? void 0 : closingSubscriber.unsubscribe();
            const b = buffer;
            buffer = [];
            b && subscriber.next(b);
            innerFrom(closingSelector()).subscribe((closingSubscriber = new OperatorSubscriber(subscriber, openBuffer, undefined, noop)));
        };
        openBuffer();
        source.subscribe(new OperatorSubscriber(subscriber, (value) => buffer === null || buffer === void 0 ? void 0 : buffer.push(value), undefined, () => {
            buffer && subscriber.next(buffer);
            subscriber.complete();
        }, () => (buffer = closingSubscriber = null)));
    });
}
//# sourceMappingURL=bufferWhen.js.map