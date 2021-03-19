import { zip as zipStatic } from '../observable/zip';
import { operate } from '../util/lift';
export function zip(...sources) {
    return operate((source, subscriber) => {
        zipStatic(source, ...sources).subscribe(subscriber);
    });
}
export function zipWith(...otherInputs) {
    return zip(...otherInputs);
}
//# sourceMappingURL=zipWith.js.map