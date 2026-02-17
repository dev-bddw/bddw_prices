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

export function hasSplit(layout) {
  return layout?.type === 'split';
}
