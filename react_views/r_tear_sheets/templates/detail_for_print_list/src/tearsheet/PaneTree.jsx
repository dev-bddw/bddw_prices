import PaneLeaf from './PaneLeaf';
import PaneSplit from './PaneSplit';

export default function PaneTree({ layout, path, logicalWidth, logicalHeight, gutterWidth, displayScale }) {
  if (!layout) return null;

  if (layout.type === 'leaf') {
    return (
      <PaneLeaf
        leaf={layout}
        logicalWidth={logicalWidth}
        logicalHeight={logicalHeight}
      />
    );
  }

  if (layout.type === 'split') {
    return (
      <PaneSplit
        node={layout}
        path={path}
        logicalWidth={logicalWidth}
        logicalHeight={logicalHeight}
        gutterWidth={gutterWidth}
        displayScale={displayScale}
      />
    );
  }

  return null;
}
