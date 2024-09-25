export const resizeImage = (file: Blob, maxWidth: number, maxHeight: number): Promise<string> => {
  return new Promise((resolve, reject) => {
***REMOVED***const img = new Image()
***REMOVED***const reader = new FileReader()

***REMOVED***reader.readAsDataURL(file)
***REMOVED***reader.onloadend = () => {
***REMOVED***  img.src = reader.result as string
***REMOVED***  img.onload = () => {
***REMOVED***const canvas = document.createElement('canvas')
***REMOVED***const ctx = canvas.getContext('2d')

***REMOVED***let { width, height } = img

***REMOVED***// Calculate the new dimensions
***REMOVED***if (width > maxWidth || height > maxHeight) {
***REMOVED***  if (width > height) {
***REMOVED******REMOVED***height = (maxWidth / width) * height
***REMOVED******REMOVED***width = maxWidth
  ***REMOVED***
***REMOVED******REMOVED***width = (maxHeight / height) * width
***REMOVED******REMOVED***height = maxHeight
  ***REMOVED***
***REMOVED***

***REMOVED***canvas.width = width
***REMOVED***canvas.height = height

***REMOVED***if (ctx) {
***REMOVED***  ctx.drawImage(img, 0, 0, width, height)
***REMOVED***

***REMOVED***// Convert the canvas to a base64 string
***REMOVED***const resizedBase64 = canvas.toDataURL('image/jpeg', 0.8)
***REMOVED***resolve(resizedBase64)
  ***REMOVED***

***REMOVED***  img.onerror = error => {
***REMOVED***reject('Error loading image: ' + error)
  ***REMOVED***
***REMOVED***

***REMOVED***reader.onerror = error => {
***REMOVED***  reject('Error reading file: ' + error)
***REMOVED***
  })
}
