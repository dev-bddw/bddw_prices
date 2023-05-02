import { useState, useRef, useEffect } from 'react';
import SETTINGS from './Settings'

export default function Nav() {

	const links = [
		{
		'name': 'VIEW PDF',
		'href': CONTEXT.print,
		},
		{
		'name': 'DOWNLOAD PDF',
		'href': CONTEXT.print + '?justDownload=True',
	  },
		{
		'name': 'VIEW LIST PDF',
		'href': CONTEXT.print_list,
		},
		{
		'name': 'DOWNLOAD LIST PDF',
		'href': CONTEXT.print_list + '?justDownload=True',
		},
		{
		'name': 'EDIT',
		'href': CONTEXT.edit_tearsheet,
		}
	]


	return (
		<>
			<a className="text-left text-xs" href={CONTEXT.tearsheets_list}>{'<<<'} list</a>
			<div className="text-right text-xs">
			{ links.map( (link) => { return( <><a href={link.href} className="px-1 text-gray-500 text-right">{link.name}</a>-</> )})}
			</div>
	</>
	)
}
