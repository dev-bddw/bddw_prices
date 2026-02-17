import PaneLeaf from './PaneLeaf';
import PaneSplit from './PaneSplit';

export default function PaneTree({
  layout,
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
  if (!layout) return null;

  if (layout.type === 'leaf') {
    return (
      <PaneLeaf
        path={path}
        leaf={layout}
        logicalWidth={logicalWidth}
        logicalHeight={logicalHeight}
        isSelected={selectedPath && path.length === selectedPath.length && path.every((p, i) => p === selectedPath[i])}
        onSelect={onSelect}
        editMode={editMode}
        onUploadImage={onUploadImage}
        displayScale={displayScale}
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
        selectedPath={selectedPath}
        onSelect={onSelect}
        onLayoutChange={onLayoutChange}
        editMode={editMode}
        onUploadImage={onUploadImage}
        gutterWidth={gutterWidth}
        displayScale={displayScale}
      />
    );
  }

  return null;
}
