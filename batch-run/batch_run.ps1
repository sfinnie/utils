$inputPath=".\inputs\"
$outputPath=".\outputs\"

$files=Get-ChildItem $inputPath

foreach ($file in $files)
{
    # write-host $file
    $src = $inputPath + $file
    $dest = $outputPath + $file
    # Copy-Item $src $dest
    magick convert -format "jpg" -strip $src $dest
    write-host $dest
}