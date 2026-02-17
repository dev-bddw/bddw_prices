import { useCallback, useState } from 'react';
import PaneTree from './PaneTree';

const RATIO_MIN = 0.1;
const RATIO_MAX = 0.9;

export default function PaneSplit({
  node,
  path,
  logicalWidth,
  logicalHeight,
  selectedPath,
  onSelect,
  onLayoutChange,
  editMode,
  onUploadImage,
  gutterWidth,
  displayScale,
}) {
  const { direction, ratio, children } = node;
  const gw = gutterWidth ?? 8;
  const isHorizontal = direction === 'horizontal';
  const total = isHorizontal ? logicalHeight : logicalWidth;
  const firstSize = Math.max(0, Math.round((total - gw) * ratio));
  const secondSize = Math.max(0, total - gw - firstSize);

  const [isDragging, setIsDragging] = useState(false);

  const updateRatio = useCallback(
    (newRatio) => {
      const clamped = Math.max(RATIO_MIN, Math.min(RATIO_MAX, newRatio));
      onLayoutChange(path, (split) => ({ ...split, ratio: clamped }));
    },
    [path, onLayoutChange]
  );

  const handleGutterMouseDown = useCallback(
    (e) => {
      if (!editMode) return;
      e.preventDefault();
      setIsDragging(true);
      const startClient = isHorizontal ? e.clientY : e.clientX;
      const startRatio = ratio;
      const logicalTotal = total - gw;

      const onMove = (moveEvent) => {
        const currentClient = isHorizontal ? moveEvent.clientY : moveEvent.clientX;
        const deltaScreen = currentClient - startClient;
        const deltaLogical = deltaScreen / displayScale;
        const deltaRatio = logicalTotal > 0 ? deltaLogical / logicalTotal : 0;
        const newRatio = startRatio + deltaRatio;
        updateRatio(newRatio);
      };

      const onUp = () => {
        setIsDragging(false);
        window.removeEventListener('mousemove', onMove);
        window.removeEventListener('mouseup', onUp);
      };

      window.addEventListener('mousemove', onMove);
      window.addEventListener('mouseup', onUp);
    },
    [editMode, isHorizontal, ratio, total, gw, displayScale, updateRatio]
  );

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
        selectedPath={selectedPath}
        onSelect={onSelect}
        onLayoutChange={onLayoutChange}
        editMode={editMode}
        onUploadImage={onUploadImage}
        gutterWidth={gutterWidth}
        displayScale={displayScale}
      />
      <div
        role="separator"
        aria-label={isHorizontal ? 'Drag to resize panes vertically' : 'Drag to resize panes horizontally'}
        onMouseDown={handleGutterMouseDown}
        title={editMode ? (isHorizontal ? 'Drag gutter up or down' : 'Drag gutter left or right') : undefined}
        style={{
          width: isHorizontal ? logicalWidth : gw,
          height: isHorizontal ? gw : logicalHeight,
          minWidth: isHorizontal ? 0 : gw,
          minHeight: isHorizontal ? gw : 0,
          background: 'white',
          border: '1px solid rgba(0,0,0,0.06)',
          boxSizing: 'border-box',
          cursor: editMode ? (isHorizontal ? 'ns-resize' : 'ew-resize') : 'default',
          flexShrink: 0,
          userSelect: 'none',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {editMode && gw >= 6 && (
          <div
            style={{
              width: isHorizontal ? 24 : 4,
              height: isHorizontal ? 4 : 24,
              background: 'rgba(0,0,0,0.12)',
              borderRadius: 2,
              pointerEvents: 'none',
            }}
            aria-hidden
          />
        )}
      </div>
      <PaneTree
        layout={children[1]}
        path={[...path, 1]}
        logicalWidth={secondWidth}
        logicalHeight={secondHeight}
        selectedPath={selectedPath}
        onSelect={onSelect}
        onLayoutChange={onLayoutChange}
        editMode={editMode}
        onUploadImage={onUploadImage}
        gutterWidth={gutterWidth}
        displayScale={displayScale}
      />
    </div>
  );
}
