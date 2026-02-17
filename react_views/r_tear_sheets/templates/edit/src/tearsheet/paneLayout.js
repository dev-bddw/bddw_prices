/**
 * Pane layout tree helpers. Max depth 2 splits (4 leaf panes).
 * Leaf: { type: 'leaf', imageUrl, image_scale, image_offset_x, image_offset_y }
 * Split: { type: 'split', direction: 'horizontal'|'vertical', ratio: number, children: [node, node] }
 */

export function createDefaultLeaf(imageUrl = null) {
  return {
    type: 'leaf',
    imageUrl,
    image_scale: 1,
    image_offset_x: 0,
    image_offset_y: 0,
  };
}

export function createLegacyLeaf(img, image_scale = 1, image_offset_x = 0, image_offset_y = 0) {
  return {
    type: 'leaf',
    imageUrl: img || null,
    image_scale: Number(image_scale) || 1,
    image_offset_x: Number(image_offset_x) || 0,
    image_offset_y: Number(image_offset_y) || 0,
  };
}

export function createDefaultSplit(direction, ratio = 0.5) {
  return {
    type: 'split',
    direction,
    ratio,
    children: [createDefaultLeaf(), createDefaultLeaf()],
  };
}

export function getNodeAtPath(layout, path) {
  if (!layout || path.length === 0) return layout;
  let node = layout;
  for (let i = 0; i < path.length; i++) {
    const idx = path[i];
    if (node.type === 'split' && node.children && node.children[idx] !== undefined) {
      node = node.children[idx];
    } else {
      return undefined;
    }
  }
  return node;
}

export function getLeafAtPath(layout, path) {
  const node = getNodeAtPath(layout, path);
  return node?.type === 'leaf' ? node : undefined;
}

function setNodeAtPath(layout, path, updater) {
  if (!layout || path.length === 0) return updater(layout);
  const [idx, ...rest] = path;
  if (layout.type !== 'split' || !layout.children) return layout;
  const next = setNodeAtPath(layout.children[idx], rest, updater);
  const children = [...layout.children];
  children[idx] = next;
  return { ...layout, children };
}

export function setLeafAtPath(layout, path, leafData) {
  return setNodeAtPath(layout, path, (node) => {
    if (node?.type !== 'leaf') return node;
    return { ...node, ...leafData };
  });
}

export function setSplitAtPath(layout, path, splitData) {
  return setNodeAtPath(layout, path, (node) => {
    if (node?.type !== 'split') return node;
    return { ...node, ...splitData };
  });
}

export function canSplit(layout, path) {
  if (!layout) return false;
  if (path.length >= 2) return false; // max depth 2
  const node = getNodeAtPath(layout, path);
  return node?.type === 'leaf';
}

export function replaceLeafWithSplit(layout, path, direction) {
  if (!canSplit(layout, path)) return layout;
  const leaf = getLeafAtPath(layout, path);
  const newSplit = createDefaultSplit(direction);
  // Preserve first child with current leaf image/transform when splitting
  if (leaf) {
    newSplit.children[0] = { ...createDefaultLeaf(leaf.imageUrl), ...leaf };
  }
  return setNodeAtPath(layout, path, () => newSplit);
}

export function hasSplit(layout) {
  return layout?.type === 'split';
}

export function updateNodeAtPath(layout, path, updater) {
  if (!layout || path.length === 0) return updater(layout);
  const [idx, ...rest] = path;
  if (layout.type !== 'split' || !layout.children) return layout;
  const next = updateNodeAtPath(layout.children[idx], rest, updater);
  const children = [...layout.children];
  children[idx] = next;
  return { ...layout, children };
}
