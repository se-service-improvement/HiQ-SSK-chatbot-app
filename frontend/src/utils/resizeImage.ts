export const resizeImage = (file: Blob, maxWidth: number, maxHeight: number) => {
  const img = new Image()
  const reader = new FileReader()

  reader.readAsDataURL(file)
  reader.onloadend = () => {
***REMOVED***img.src = reader.result as string
***REMOVED***img.onload = () => {
***REMOVED***  const canvas = document.createElement('canvas')
***REMOVED***  const ctx = canvas.getContext('2d')

***REMOVED***  let { width, height } = img

***REMOVED***  if (width > maxWidth || height > maxHeight) {
***REMOVED***if (width > height) {
***REMOVED***  height *= maxWidth / width
***REMOVED***  width = maxWidth
***REMOVED***
***REMOVED***  width *= maxHeight / height
***REMOVED***  height = maxHeight
***REMOVED***
  ***REMOVED***

***REMOVED***  canvas.width = width
***REMOVED***  canvas.height = height
***REMOVED***  if (ctx) {
***REMOVED***ctx.drawImage(img, 0, 0, width, height)
  ***REMOVED***

***REMOVED***  const resizedBase64 = canvas.toDataURL('image/jpeg', 0.8)
***REMOVED***  return resizedBase64
***REMOVED***
  }
  reader.onerror = error => {
***REMOVED***console.error('Error: ', error)
  }
}
