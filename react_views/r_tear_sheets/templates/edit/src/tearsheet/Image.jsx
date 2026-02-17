import { useState, useRef, useEffect } from 'react';

// Fixed frame size used in both edit and detail so image displays identically (1500×1200)
const IMAGE_FRAME_WIDTH = 1500;
const IMAGE_FRAME_HEIGHT = 1200;
// Content column width; scale frame to fit
const COLUMN_WIDTH = 816;
const DISPLAY_SCALE = COLUMN_WIDTH / IMAGE_FRAME_WIDTH;
const DISPLAY_HEIGHT = Math.round(IMAGE_FRAME_HEIGHT * DISPLAY_SCALE);

export default function Image({ img, imageTransform }) {

	const [ img_url, setImgUrl] = useState(img)
	const [ img_data, setImgData] = useState()
	const isMounted = useRef(false)
	const hiddenFileInput = useRef(null)

	const scale = imageTransform?.image_scale != null ? Math.max(1, Number(imageTransform.image_scale)) : 1
	const offsetX = imageTransform?.image_offset_x != null ? Number(imageTransform.image_offset_x) : 0
	const offsetY = imageTransform?.image_offset_y != null ? Number(imageTransform.image_offset_y) : 0

	function handleClick(event) {
		// use refs to programmatically use default behavior https://blog.logrocket.com/complete-guide-react-refs/
		hiddenFileInput.current.click();
	}

	function onChangeHandler(event) {
		setImgData(event.target.files[0])
	}


	// add a delay, then execute the api call on cleanup
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
			if (isMounted.current) {
			  POST()
			} else {
					isMounted.current = true
				}
    }, 1500)
		return( () => clearTimeout(delayDebounceFn) )
  }, [img_data])


	const POST = () => {

		let form_data = new FormData();
		form_data.append('image', img_data)

		fetch(CONTEXT.edit_image_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
						},
			body: form_data
					})
						.then(response => {
							if (!response.ok) return response.json().then(data => { throw new Error(data.error || response.statusText) });
							return response.json();
						})
						.then(data => { if (data.url) setImgUrl(data.url); } )
						.catch(err => console.error('Image upload failed:', err))
	}

	return (
		<div style={{ maxWidth: COLUMN_WIDTH }}>
				<div
					onClick={(event) => { handleClick(event); }}
					className="cursor-pointer relative"
					style={{
						width: img_url ? COLUMN_WIDTH : '100%',
						height: img_url ? DISPLAY_HEIGHT : 200,
						minHeight: img_url ? DISPLAY_HEIGHT : 200,
						overflow: 'hidden',
						position: 'relative',
					}}
				>
					{img_url ? (
						<div
							style={{
								position: 'absolute',
								left: 0,
								top: 0,
								width: IMAGE_FRAME_WIDTH,
								height: IMAGE_FRAME_HEIGHT,
								transform: `scale(${DISPLAY_SCALE})`,
								transformOrigin: '0 0',
							}}
						>
							<div
								className="hover:opacity-90"
								style={{
									position: 'absolute',
									left: '50%',
									top: '50%',
									width: '100%',
									height: '100%',
									backgroundImage: `url(${img_url})`,
									backgroundSize: 'cover',
									backgroundPosition: 'center',
									transformOrigin: 'center',
									transform: `translate(-50%, -50%) translate(${offsetX}px, ${offsetY}px) scale(${scale})`,
								}}
							/>
						</div>
					) : (
						<div className="flex items-center justify-center bg-gray-200 min-h-[200px] text-gray-500">Click to add image</div>
					)}
					<input style={{'display': 'none'}} ref={hiddenFileInput} type="file" name="image_url" accept="image/jpeg,image/png,image/gif" onChange={(event) => {onChangeHandler(event)}}></input>
					<p className="opacity-25 hover:opacity-100 duration-300 absolute text-5xl underline text-white top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">Change Image</p>
				</div>
		</div>
	)
}
