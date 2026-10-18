// Original teaching fixture; not a model of a production implementation.
method FirstIndex(values: seq<int>, target: int) returns (index: int)
  ensures -1 <= index < |values|
  ensures index == -1 <==> target !in values
  ensures index >= 0 ==> values[index] == target
  ensures index >= 0 ==> target !in values[..index]
{
  var i := 0;
  while i < |values|
    invariant 0 <= i <= |values|
    invariant forall j :: 0 <= j < i ==> values[j] != target
    decreases |values| - i
  {
    if values[i] == target {
      return i;
    }
    i := i + 1;
  }
  return -1;
}

method Main()
{
  var empty := FirstIndex([], 7);
  assert empty == -1;
  var singleton := FirstIndex([7], 7);
  assert singleton == 0;
  var duplicate := FirstIndex([4, 7, 7], 7);
  assert [4, 7, 7][..2] == [4, 7];
  assert duplicate == 1;
  var last := FirstIndex([4, 7], 7);
  assert last == 1;
  var missing := FirstIndex([4, 5], 7);
  assert missing == -1;
  print empty, " ", singleton, " ", duplicate, " ", last, " ", missing, "\n";
}
