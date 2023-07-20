function returnCategories(arr) {
    const categories = arr.map( (pr) => { return(pr.category) } )
    const unique = categories.filter((value, index, self) => {
      return self.indexOf(value) == index;
    })
    return unique
    }


function processContext(arr) {

    const return_by_si = (si) => {
      const by_si = arr.filter( (pr) => pr.series_item == si )
      return by_si
    }

    const getSeriesItemList = (arr) => {
      const series_items = arr.map( (pr) => { return(pr.series_item) } )
      const unique = series_items.filter((value, index, self) => {
        return self.indexOf(value) == index;
      })
      return unique
      }

    const pricelist_arr = getSeriesItemList(arr).map( (series_item) => {
      let this_obj = {}
      this_obj['series_item'] = series_item
      this_obj['category'] = return_by_si(series_item)[0].category
      this_obj['price_records'] = return_by_si(series_item)
      this_obj['order'] = categoryOrder[return_by_si(series_item)[0].category]
      return this_obj
    })

    pricelist_arr.sort( (a,b)=> {
      if ( a.order > b.order) {
        return 1
      } else if ( categoryOrder[a.category] == categoryOrder[b.category]) {
        return 0
      } else {
        return -1
      }
    }
    )

    return pricelist_arr
  }

const categoryOrder = {
  'DINING TABLES': 1,
  'STORAGE': 2,
  'CONSOLE TABLES': 3,
  'SHELVING': 4,
  'DESKS': 5,
  'COFFEE TABLES': 6,
  'SIDE TABLES': 7,
  'SEATING': 8,
  'BENCHES': 9,
  'UPHOLSTERY': 10,
  'LIGHTING': 11,
  'MIRRORS': 12,
  'BEDS': 13,
  'PUZZLES': 14,
  'MISCELLANEOUS': 15,
  'ROSEVALE': 16,
}

export {categoryOrder, processContext, returnCategories};
