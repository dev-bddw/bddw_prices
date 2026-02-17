import { useRef } from 'react';

export default function PaneLeaf({
  path,
  leaf,
  logicalWidth,
  logicalHeight,
  isSelected,
  onSelect,
  editMode,
  onUploadImage,
  displayScale,
}) {
  const hiddenFileInput = useRef(null);
  const scale = leaf?.image_scale != null ? Math.max(1, Number(leaf.image_scale)) : 1;
  const offsetX = leaf?.image_offset_x != null ? Number(leaf.image_offset_x) : 0;
  const offsetY = leaf?.image_offset_y != null ? Number(leaf.image_offset_y) : 0;
  const imageUrl = leaf?.imageUrl ?? null;

  const handleClick = (e) => {
    e.stopPropagation();
    if (editMode) {
      onSelect(path);
      if (e.target === hiddenFileInput.current || e.target.closest('input[type="file"]')) return;
      if (!imageUrl) hiddenFileInput.current?.click();
    }
  };

  const handleAddImageClick = (e) => {
    e.stopPropagation();
    hiddenFileInput.current?.click();
  };

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={handleClick}
      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleClick(e); } }}
      style={{
        width: logicalWidth,
        height: logicalHeight,
        overflow: 'hidden',
        position: 'relative',
        border: isSelected ? '3px solid #2563eb' : '1px solid transparent',
        boxSizing: 'border-box',
        cursor: editMode ? 'pointer' : 'default',
      }}
    >
      {imageUrl ? (
        <div
          className={editMode ? 'hover:opacity-90' : ''}
          style={{
            position: 'absolute',
            left: '50%',
            top: '50%',
            width: '100%',
            height: '100%',
            backgroundImage: `url(${imageUrl})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            transformOrigin: 'center',
            transform: `translate(-50%, -50%) translate(${offsetX}px, ${offsetY}px) scale(${scale})`,
          }}
        />
      ) : (
        <div
          style={{
            width: '100%',
            height: '100%',
            background: '#e5e7eb',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#6b7280',
            fontSize: 14,
          }}
        >
          {editMode ? 'Click to add image' : ''}
        </div>
      )}
      {editMode && (
        <>
          <input
            ref={hiddenFileInput}
            type="file"
            accept="image/jpeg,image/png,image/gif"
            style={{ display: 'none' }}
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) onUploadImage(path, file);
              e.target.value = '';
            }}
          />
          {imageUrl && (
            <div
              onClick={(e) => { e.stopPropagation(); handleAddImageClick(e); }}
              style={{
                position: 'absolute',
                bottom: 4,
                right: 4,
                background: 'rgba(0,0,0,0.6)',
                color: 'white',
                padding: '4px 8px',
                borderRadius: 4,
                fontSize: 12,
                cursor: 'pointer',
              }}
            >
              Change image
            </div>
          )}
        </>
      )}
    </div>
  );
}
