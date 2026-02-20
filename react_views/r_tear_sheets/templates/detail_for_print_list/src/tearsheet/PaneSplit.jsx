import PaneTree from './PaneTree';

export default function PaneSplit({ node, path, logicalWidth, logicalHeight, gutterWidth, displayScale }) {
  const { direction, ratio, children } = node;
  const gw = gutterWidth ?? 8;
  const isHorizontal = direction === 'horizontal';
  const total = isHorizontal ? logicalHeight : logicalWidth;
  const firstSize = Math.max(0, Math.round((total - gw) * ratio));
  const secondSize = Math.max(0, total - gw - firstSize);

  const firstWidth = isHorizontal ? logicalWidth : firstSize;
  const firstHeight = isHorizontal ? firstSize : logicalHeight;
  const secondWidth = isHorizontal ? logicalWidth : secondSize;
  const secondHeight = isHorizontal ? secondSize : logicalHeight;

  return (
    <div
      style={{
        width: logicalWidth,
        height: logicalHeight,
        display: 'flex',
        flexDirection: isHorizontal ? 'column' : 'row',
      }}
    >
      <PaneTree
        layout={children[0]}
        path={[...path, 0]}
        logicalWidth={firstWidth}
        logicalHeight={firstHeight}
        gutterWidth={gutterWidth}
        displayScale={displayScale}
      />
      <div
        style={{
          width: isHorizontal ? logicalWidth : gw,
          height: isHorizontal ? gw : logicalHeight,
          minWidth: isHorizontal ? 0 : gw,
          minHeight: isHorizontal ? gw : 0,
          background: 'white',
          border: 'none',
          flexShrink: 0,
        }}
      />
      <PaneTree
        layout={children[1]}
        path={[...path, 1]}
        logicalWidth={secondWidth}
        logicalHeight={secondHeight}
        gutterWidth={gutterWidth}
        displayScale={displayScale}
      />
    </div>
  );
}
